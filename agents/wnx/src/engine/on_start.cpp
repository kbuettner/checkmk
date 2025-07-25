// Configuration Parameters for whole Agent
#include "stdafx.h"

#include "wnx/on_start.h"

#include <atomic>
#include <string>

#include "common/cfg_info.h"
#include "tools/_process.h"
#include "wnx/cfg.h"
#include "wnx/cfg_details.h"
#include "wnx/cma_core.h"
#include "wnx/install_api.h"
#include "wnx/windows_service_api.h"

namespace fs = std::filesystem;

namespace cma {

bool OnStart(AppType proposed_type, const std::wstring &config_file);
inline bool OnStart(AppType type) { return OnStart(type, L""); }
bool OnStartApp() { return OnStart(AppType::automatic); }
bool OnStartTest() { return OnStart(AppType::test); }

// internal global variables:
namespace {
bool g_config_loaded = false;
std::atomic g_s_on_start_called = false;
}  // namespace

bool ConfigLoaded() { return g_config_loaded; }

std::pair<fs::path, fs::path> FindTestDirs(const fs::path &base) {
    auto root_dir = fs::path{base} / "test" / "root";
    auto data_dir = fs::path{base} / "test" / "data";

    if (std::error_code ec;
        fs::exists(root_dir, ec) && fs::exists(data_dir, ec)) {
        return {root_dir, data_dir};
    }

    return {};
}

std::pair<fs::path, fs::path> FindAlternateDirs(AppType app_type) {
    switch (app_type) {
        case AppType::exe:
            for (const auto &env_var :
                 {env::regression_base_dir, env::integration_base_dir}) {
                if (auto dir = tools::win::GetEnv(env_var); !dir.empty()) {
                    XLOG::l.i(
                        "YOU ARE USING '{}' set by environment variable '{}'",
                        wtools::ToUtf8(dir), wtools::ToUtf8(env_var));
                    return FindTestDirs(dir);
                }
            }
            break;

        case AppType::test: {
            const auto &dir = tools::win::GetEnv(env::unit_base_dir);
            if (dir.empty()) {
                XLOG::l.i(
                    "Environment variable '{}' not found, fallback to SOLUTION_DIR",
                    wtools::ToUtf8(env::unit_base_dir));
                return {fs::path{SOLUTION_DIR} / "install" / "resources", {}};
            }
            return FindTestDirs(dir);
        }
        case AppType::failed:
        case AppType::srv:
        case AppType::automatic:
            XLOG::l("Bad Mode [{}]", static_cast<int>(app_type));
            return {};
    }
    return {};
}

namespace cfg {

void LogFolders() {
    auto root_dir = GetCfg().getRootDir();
    auto data_dir = GetCfg().getDataDir();
    XLOG::l.t("Using root = '{}' and data = '{}' folders ", root_dir, data_dir);
}

bool FindAndPrepareWorkingFolders(AppType app_type) {
    switch (app_type) {
        case AppType::exe:
            [[fallthrough]];
        case AppType::test: {  // watest32
            auto [r, d] = FindAlternateDirs(app_type);
            GetCfg().initFolders(L"", r.wstring(), d.wstring());
            break;
        }
        case AppType::srv:
            if (install::IsCleanInstallationRequired()) {
                install::RemoveCleanInstallationFlag();
                try {
                    auto data_dir = fs::path(tools::win::GetSomeSystemFolder(
                                        FOLDERID_ProgramData)) /
                                    kAppDataCompanyName / kAppDataAppName;
                    XLOG::l.i(
                        "Clean installation is required, removing old files from {}",
                        data_dir);
                    std::error_code ec;
                    fs::remove_all(data_dir, ec);
                } catch (const std::exception &e) {
                    XLOG::details::LogWindowsEventError(
                        102, "Exception during clean installation {}",
                        e.what());
                }
            }
            GetCfg().initFolders(cma::srv::kServiceName, L"", L"");
            break;
        case AppType::automatic:
            [[fallthrough]];
        case AppType::failed:
            XLOG::l.crit("Invalid value of the AppType automatic [{}]",
                         static_cast<int>(app_type));
            return false;
    }
    LogFolders();
    return true;
}

}  // namespace cfg

static AppType CalcAppType(AppType app_type) {
    if (app_type == AppType::automatic) {
        return AppDefaultType();
    }

    if (app_type == AppType::test) {
        details::SetModus(Modus::test);
    }

    return app_type;
}

bool ReloadConfig() {
    //
    return LoadConfigFull({});
}

UninstallAlert g_uninstall_alert;

// usually for testing
void UninstallAlert::clear() noexcept {
    //
    set_ = false;
}

void UninstallAlert::set() noexcept {
    //
    if (GetModus() != Modus::service) {
        XLOG::l.i("Requested clean on exit is IGNORED, not service");
        return;
    }

    XLOG::l.i("Requested clean on exit");
    XLOG::details::LogWindowsEventAlways(XLOG::EventLevel::information, 9,
                                         "Requested Clean On Exit");
    set_ = true;
}

bool LoadConfigBase(const std::vector<std::wstring> &config_filenames,
                    YamlCacheOp cache_op) {
    g_config_loaded = cfg::InitializeMainConfig(config_filenames, cache_op);

    if (g_config_loaded) {
        cfg::ProcessKnownConfigGroups();
        cfg::SetupEnvironmentFromGroups();
    }

    XLOG::l.i("Loaded start config {}",
              wtools::ToUtf8(cfg::GetPathOfLoadedConfig()));
    return true;
}

bool LoadConfigFull(const std::wstring &config_file) {
    cfg::details::KillDefaultConfig();
    // load config is here
    auto cfg_files = cfg::DefaultConfigArray();
    if (!config_file.empty()) {
        cfg_files.clear();
        cfg_files.push_back(config_file);
    }

    return LoadConfigBase(cfg_files, YamlCacheOp::update);
}

bool OnStartCore(AppType type, const std::wstring &config_file) {
    if (!cfg::FindAndPrepareWorkingFolders(type)) {
        return false;
    }
    wtools::InitWindowsCom();

    return LoadConfigFull(config_file);
}

/// must be called on the start
bool OnStart(AppType proposed_type, const std::wstring &config_file) {
    const auto type = CalcAppType(proposed_type);

    const auto already_loaded = g_s_on_start_called.exchange(true);
    if (type == AppType::srv) {
        XLOG::details::LogWindowsEventAlways(XLOG::EventLevel::information, 35,
                                             "check_mk_service is loading");
    }

    if (!already_loaded) {
        XLOG::setup::SetContext(GetModus() == Modus::service ? "srv" : "app");
        return OnStartCore(type, config_file);
    }

    if (AppDefaultType() == AppType::test) {
        XLOG::d.i("Second call of OnStart in test mode");
        return OnStartCore(type, config_file);
    }

    XLOG::l.crit(
        "Second call of OnStart, this may happen ONLY in test environment");

    return true;
}

void OnExit() {
    if (wtools::IsWindowsComInitialized()) wtools::CloseWindowsCom();
}
}  // namespace cma
