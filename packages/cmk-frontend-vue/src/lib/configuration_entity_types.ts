/**
 * Copyright (C) 2024 Checkmk GmbH - License: GNU General Public License v2
 * This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
 * conditions defined in the file COPYING, which is part of this source code package.
 */
import type { ValidationMessage } from 'cmk-shared-typing/typescript/vue_formspec_components'

export type ValidationMessages = ValidationMessage[]

export type SetDataResult<Result> =
  | { type: 'success'; entity: Result }
  | { type: 'error'; validationMessages: ValidationMessages }
