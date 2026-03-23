/**
 * Copyright (C) 2025 Checkmk GmbH - License: Checkmk Enterprise License
 * This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
 * conditions defined in the file COPYING, which is part of this source code package.
 */
import {
  type Query as GraphLineQuery,
  type GraphLines,
  type GraphOptions
} from 'cmk-shared-typing/typescript/graph_designer'

import { cmkAjax } from '@/lib/ajax'

// Copied from cmk-frontend/src/js/modules/graphs.ts

type SizePT = number

interface GraphDisplayConfig {
  fixed_timerange: boolean
  font_size: SizePT
  foreground_color: string
  interaction: boolean
  onclick: string | null
  preview: boolean
  resizable: boolean
  show_controls: boolean
  show_pin: boolean
  show_time_axis: boolean
  show_time_range_previews: boolean
  show_vertical_axis: boolean
  vertical_axis_width: 'fixed' | ['explicit', SizePT]
}

// eslint-disable-next-line  @typescript-eslint/no-explicit-any
type GraphRecipe = Record<string, any>

interface GraphTimeRange {
  time_range: [number, number]
}

interface GraphContext {
  graph_id: string
  recipe: GraphRecipe
  time_range: GraphTimeRange
  display_config: GraphDisplayConfig
  display_id: string
}

interface LayoutedCurveArea {
  line_type: 'area' | '-area'
  points: [number | null, number | null][]
  //dynamic
  title?: string
  color: string
}

interface LayoutedCurveStack {
  line_type: 'stack' | '-stack'
  points: [number | null, number | null][]
  //dynamic
  title?: string
  color: string
}

interface LayoutedCurveLine {
  line_type: 'line' | '-line'
  points: (number | null)[]
  //dynamic
  title?: string
  color: string
}

type LayoutedCurve = LayoutedCurveLine | LayoutedCurveArea | LayoutedCurveStack

interface HorizontalRule {
  value: number
  rendered_value: string
  color: string
  title: string
}

interface AxisTick {
  position: number
  text: string | null
  line_width: number
}

interface YAxis {
  range: [number, number]
  unit_label: string | null
  labels: AxisTick[]
  //dynamic
  pixels_per_unit: number
}

interface XAxis {
  labels: AxisTick[]
  range: [number, number]
}

//this type is from cmk/gui/plugins/metrics/artwork.py:82
interface ActualTimeRange {
  start: number
  end: number
  step: number
}

interface RequestedTimeRange {
  start: number
  end: number
}

interface GraphArtwork {
  //optional properties assigned dynamically in javascript
  id: string
  canvas_obj: HTMLCanvasElement
  display_config: GraphDisplayConfig
  time_origin?: number
  vertical_origin?: number
  // Actual data and axes
  curves: LayoutedCurve[]
  horizontal_rules: HorizontalRule[]
  y_axis: YAxis
  x_axis: XAxis
  mark_requested_end_time: boolean
  //Displayed range
  actual_time: ActualTimeRange
  requested_time: RequestedTimeRange
  requested_y_range: [number, number] | null
  pin_time: number | null
}

export interface AjaxGraph {
  html: string
  graph: GraphArtwork
  context: GraphContext
  error?: string
  warning?: string
  queries_reached_limit?: GraphLineQuery[]
}

export async function fetchAjaxGraph<OutputType>(
  graphId: string,
  graphLines: GraphLines,
  graphOptions: GraphOptions
): Promise<OutputType> {
  return cmkAjax('ajax_fetch_ajax_graph.py', {
    graph_id: graphId,
    graph_lines: graphLines,
    graph_options: graphOptions
  })
}

export type GraphRenderer = (ajaxGraph: AjaxGraph, container: HTMLDivElement) => void

export async function graphRenderer(ajaxGraph: AjaxGraph, container: HTMLDivElement) {
  // @ts-expect-error comes from different javascript file
  window['cmk'].graphs.show_ajax_graph_at_container(ajaxGraph, container)
}
