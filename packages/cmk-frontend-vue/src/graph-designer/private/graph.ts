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

interface GraphTitleFormat {
  plain: boolean
  add_host_name: boolean
  add_host_alias: boolean
  add_service_description: boolean
}

interface GraphRenderConfig {
  border_width: number
  color_gradient: number
  editing: boolean
  explicit_title: string | null
  fixed_timerange: boolean
  font_size: SizePT
  foreground_color: string
  interaction: boolean
  onclick: string | null
  preview: boolean
  resizable: boolean
  show_controls: boolean
  show_graph_time: boolean
  show_legend: boolean
  show_margin: boolean
  show_pin: boolean
  show_time_axis: boolean
  show_time_range_previews: boolean
  show_title: boolean | 'inline'
  show_vertical_axis: boolean
  size: [number, number]
  title_format: GraphTitleFormat
  vertical_axis_width: 'fixed' | ['explicit', SizePT]
}

// eslint-disable-next-line  @typescript-eslint/no-explicit-any
type GraphRecipe = Record<string, any>

interface AjaxContext {
  graph_id: string
  graph_recipe: GraphRecipe
  render_config: GraphRenderConfig
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
  points: number | null[]
  //dynamic
  title?: string
  color: string
}

type LayoutedCurve = LayoutedCurveLine | LayoutedCurveArea | LayoutedCurveStack

interface HorizontalRule {
  value: number
  color: string
  title: string
}

interface VerticalAxisLabel {
  position: number
  text: string
  line_width: number
}

interface VerticalAxis {
  range: [number, number]
  labels: VerticalAxisLabel[]
  //dynamic
  pixels_per_unit: number
}

interface TimeAxisLabel {
  position: number
  text: string | null
  line_width: number
}

interface TimeAxis {
  labels: TimeAxisLabel[]
  range: [number, number]
}

//this type is from cmk/gui/plugins/metrics/artwork.py:82
interface GraphArtwork {
  //optional properties assigned dynamically in javascript
  id: string
  canvas_obj: HTMLCanvasElement
  render_config: GraphRenderConfig
  time_origin?: number
  vertical_origin?: number
  // Actual data and axes
  curves: LayoutedCurve[]
  horizontal_rules: HorizontalRule[]
  vertical_axis: VerticalAxis
  time_axis: TimeAxis
  mark_requested_end_time: boolean
  //Displayed range
  start_time: number
  end_time: number
  step: number
  requested_vrange: [number, number] | null
  requested_start_time: number
  requested_end_time: number
  pin_time: number | null
}

export interface AjaxGraph {
  html: string
  graph: GraphArtwork
  context: AjaxContext
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
