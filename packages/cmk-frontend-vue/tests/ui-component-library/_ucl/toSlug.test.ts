/**
 * Copyright (C) 2026 Checkmk GmbH - License: GNU General Public License v2
 * This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
 * conditions defined in the file COPYING, which is part of this source code package.
 */
import { toSlug } from '@ucl/_ucl/types/page'
import { describe, expect, it } from 'vitest'

describe('toSlug', () => {
  it('converts spaces to hyphens', () => {
    expect(toSlug('My Component')).toBe('my-component')
  })

  it('lowercases the result', () => {
    expect(toSlug('MyComponent')).toBe('mycomponent')
  })

  it('handles mixed case and spaces', () => {
    expect(toSlug('Basic Elements')).toBe('basic-elements')
  })

  it('trims leading and trailing whitespace', () => {
    expect(toSlug('  Buttons  ')).toBe('buttons')
  })

  it('collapses multiple consecutive spaces into a single hyphen', () => {
    expect(toSlug('foo  bar')).toBe('foo-bar')
  })

  it('strips special URL characters', () => {
    expect(toSlug('Button & Icon')).toBe('button-icon')
    expect(toSlug('50% Off')).toBe('50-off')
    expect(toSlug('A/B Testing')).toBe('ab-testing')
    expect(toSlug('foo?bar=baz')).toBe('foobarbaz')
    expect(toSlug('hash#tag')).toBe('hashtag')
  })

  it('collapses consecutive hyphens produced by stripping special chars', () => {
    expect(toSlug('foo & bar')).toBe('foo-bar')
  })

  it('does not produce leading or trailing hyphens', () => {
    expect(toSlug('&leading')).toBe('leading')
    expect(toSlug('trailing&')).toBe('trailing')
    expect(toSlug('&both&')).toBe('both')
  })

  it('preserves existing hyphens in names', () => {
    expect(toSlug('my-component')).toBe('my-component')
  })

  it('produces the same slug for names that differ only by hyphens vs spaces', () => {
    expect(toSlug('My Component')).toBe(toSlug('My-Component'))
  })
})
