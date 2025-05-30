// Copyright (C) 2019 Checkmk GmbH - License: GNU General Public License v2
// This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
// conditions defined in the file COPYING, which is part of this source code package.

#[cfg(unix)]
use faccess::PathExt;
use std::fmt::Display;
#[cfg(unix)]
use std::path::{Path, PathBuf};

pub type AgentLabels = std::collections::HashMap<String, String>;

#[cfg(unix)]
#[derive(Clone)]
pub struct AgentChannel(std::path::PathBuf);
#[cfg(windows)]
#[derive(Clone)]
pub struct AgentChannel(String);

#[cfg(unix)]
impl std::convert::From<PathBuf> for AgentChannel {
    fn from(p: PathBuf) -> Self {
        AgentChannel(p)
    }
}

#[cfg(unix)]
impl std::convert::From<&str> for AgentChannel {
    fn from(s: &str) -> Self {
        AgentChannel(PathBuf::from(s))
    }
}

#[cfg(unix)]
impl std::convert::AsRef<Path> for AgentChannel {
    fn as_ref(&self) -> &Path {
        &self.0
    }
}

#[cfg(windows)]
impl std::convert::From<&str> for AgentChannel {
    fn from(s: &str) -> Self {
        Self(s.to_string())
    }
}

#[cfg(windows)]
impl std::convert::AsRef<String> for AgentChannel {
    fn as_ref(&self) -> &String {
        &self.0
    }
}

impl Display for AgentChannel {
    #[cfg(unix)]
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        {
            write!(f, "{}", self.0.to_string_lossy())
        }
    }

    #[cfg(windows)]
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        write!(f, "{}", self.0)
    }
}

impl AgentChannel {
    #[cfg(unix)]
    pub fn operational(&self) -> bool {
        // https://man7.org/linux/man-pages/man7/unix.7.html
        // On Linux, connecting to a stream socket object requires write permission on that socket;
        self.0.writable()
    }

    #[cfg(windows)]
    pub fn operational(&self) -> bool {
        // Todo (sk): anything to check here? Before we do anything here, we should however switch
        // to a toml config instead of command line options, st. this check can actually be done
        // for any mode
        true
    }
}

#[derive(serde::Deserialize, Clone)]
pub struct Credentials {
    pub username: String,
    pub password: String,
}
