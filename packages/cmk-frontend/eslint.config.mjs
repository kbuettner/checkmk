export default [
  {
    ignores: [
      'packages/cmk-frontend/src/js/modules/cbor_ext.*s',
      'packages/cmk-frontend/src/js/modules/colorpicker.*s',
      'packages/cmk-frontend/src/js/mobile_min.js',
      'packages/cmk-frontend/src/js/side_min.js',
      'packages/cmk-frontend/src/jquery/jquery.mobile-1.4.5.js',
      'packages/cmk-frontend/src/jquery/jquery.mobile-1.4.5.min.js',
      'packages/cmk-frontend/src/js/main_min.js',
      'packages/cmk-frontend/src/openapi/swagger-ui-3/swagger-ui-bundle.js',
      'packages/cmk-frontend/src/openapi/swagger-ui-3/swagger-ui-es-bundle.js',
      'packages/cmk-frontend/src/openapi/swagger-ui-3/swagger-ui.js',
      'packages/cmk-frontend/src/openapi/swagger-ui-3/swagger-ui-standalone-preset.js',
      'packages/cmk-frontend/src/openapi/swagger-ui-3/swagger-ui-es-bundle-core.js',
      'packages/cmk-frontend/src/openapi/redoc.standalone.js'
    ]
  },

  {
    files: ['packages/cmk-frontend/**/*.{js,mjs,cjs,ts,tsx}'],
    rules: {
      '@typescript-eslint/no-explicit-any': 'off',
      '@typescript-eslint/no-unused-vars': 'off',
      '@typescript-eslint/ban-ts-comment': 'off',
      '@typescript-eslint/no-require-imports': 'off',
      '@typescript-eslint/no-unused-expressions': 'off',
      'import/no-namespace': 'off',
      'no-unsanitized/property': 'off'
    }
  }
]
