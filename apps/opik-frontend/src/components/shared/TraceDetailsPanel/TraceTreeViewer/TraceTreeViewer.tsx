import React, { useCallback, useEffect, useMemo, useState } from "react";
import {
  ControlledTreeEnvironment,
  Tree,
  TreeItem,
  TreeItemIndex,
} from "react-complex-tree";
import { BASE_TRACE_DATA_TYPE, Span, Trace } from "@/types/traces";
import { treeRenderers } from "./treeRenderers";
import { calcDuration } from "@/lib/utils";
import { SPANS_COLORS_MAP, TRACE_TYPE_FOR_TREE } from "@/constants/traces";
import { Button } from "@/components/ui/button";
import useDeepMemo from "@/hooks/useDeepMemo";

type SpanWithMetadata = Omit<Span, "type"> & {
  type: BASE_TRACE_DATA_TYPE;
  duration: number;
  tokens?: number;
  spanColor?: string;
  startTimestamp?: number;
  maxStartTime?: number;
  maxEndTime?: number;
  maxDuration?: number;
};

type TreeData = Record<string, TreeItem<SpanWithMetadata>>;

type TraceTreeViewerProps = {
  trace: Trace;
  spans?: Span[];
  rowId: string;
  onSelectRow: (id: string) => void;
};

const TraceTreeViewer: React.FunctionComponent<TraceTreeViewerProps> = ({
  trace,
  spans,
  rowId,
  onSelectRow,
}) => {
  const traceSpans = useMemo(() => spans ?? [], [spans]);

  const [expandedTraceSpans, setExpandedTraceSpans] = useState<TreeItemIndex[]>(
    [],
  );

  const isAllExpended = traceSpans.length + 1 === expandedTraceSpans.length;

  const spanIds = useDeepMemo(() => {
    return traceSpans.map((chain: Span) => chain.id).sort();
  }, [traceSpans]);

  const expendAll = useCallback(
    (expand: boolean) => {
      setExpandedTraceSpans(expand ? [trace.id, ...spanIds] : []);
    },
    [trace.id, spanIds],
  );

  const toggleExpandAll = useCallback(() => {
    expendAll(!isAllExpended);
  }, [expendAll, isAllExpended]);

  useEffect(() => {
    expendAll(true);
    // we want to expand all items in tree only in case the trace is changed
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [trace.id, spanIds]);

  const treeData = useMemo(() => {
    const sharedData = {
      maxStartTime: new Date(trace.start_time).getTime(),
      maxEndTime: new Date(trace.end_time).getTime(),
      maxDuration: calcDuration(trace.start_time, trace.end_time),
    };

    const acc: TreeData = {
      root: {
        canMove: false,
        canRename: false,
        children: [trace.id],
        isFolder: true,
      } as TreeItem<never>,
      [trace.id]: {
        canMove: false,
        canRename: false,
        index: trace.id,
        isFolder: true,
        children: [],
        data: {
          ...trace,
          spanColor: SPANS_COLORS_MAP[TRACE_TYPE_FOR_TREE],
          parent_span_id: "",
          trace_id: trace.id,
          type: TRACE_TYPE_FOR_TREE,
          tokens: trace.usage?.total_tokens,
          duration: calcDuration(trace.start_time, trace.end_time),
          name: trace.name,
        },
      },
    };

    const retVal = traceSpans
      .sort((s1, s2) => s1.start_time.localeCompare(s2.start_time))
      .reduce<TreeData>((accumulator, span: Span) => {
        const spanColor = SPANS_COLORS_MAP[span.type];
        return {
          ...accumulator,
          [span.id]: {
            canMove: false,
            canRename: false,
            data: {
              ...span,
              ...sharedData,
              spanColor,
              tokens: span.usage?.total_tokens,
              duration: calcDuration(span.start_time, span.end_time),
              startTimestamp: new Date(span.start_time).getTime(),
            },
            isFolder: true,
            index: span.id,
            children: [],
          },
        };
      }, acc);

    traceSpans.forEach((span: Span) => {
      const directParentKey = span.parent_span_id;

      if (!directParentKey) {
        retVal[trace.id]?.children?.push(span.id);
      } else if (retVal[directParentKey]) {
        retVal[directParentKey].children?.push(span.id);
      }
      return retVal;
    }, acc);

    return retVal;
  }, [trace, traceSpans]);

  const viewState = useMemo(
    () => ({
      ["trace-view"]: {
        focusedItem: rowId,
        expandedItems: expandedTraceSpans,
      },
    }),
    [rowId, expandedTraceSpans],
  );

  return (
    <div className="size-full max-w-full overflow-auto py-4">
      <div className="min-w-[400px] max-w-full overflow-x-hidden">
        <div className="flex flex-row items-end gap-2 px-6 py-2">
          <div className="comet-title-m">Trace spans</div>
          <div className="comet-body-s pb-[3px] text-muted-slate">
            <div>{traceSpans.length} spans</div>
          </div>
        </div>
        <div className="px-4 py-2">
          <Button onClick={toggleExpandAll} variant="ghost" size="sm">
            {isAllExpended ? "Collapse all" : "Expand all"}
          </Button>
        </div>

        <ControlledTreeEnvironment
          items={treeData}
          onFocusItem={(item) => onSelectRow(item.index as string)}
          viewState={viewState}
          onExpandItem={(item) =>
            setExpandedTraceSpans((prev) => [...prev, item.index])
          }
          onCollapseItem={(item) =>
            setExpandedTraceSpans(
              expandedTraceSpans.filter(
                (expandedItemIndex) => expandedItemIndex !== item.index,
              ),
            )
          }
          renderDepthOffset={treeRenderers.renderDepthOffset}
          renderTreeContainer={treeRenderers.renderTreeContainer}
          renderItemsContainer={treeRenderers.renderItemsContainer}
          renderItem={treeRenderers.renderItem}
          renderItemArrow={treeRenderers.renderItemArrow}
          getItemTitle={(item) => item.data.name}
        >
          <Tree treeId="trace-view" rootItem={"root"} treeLabel="Trace tree" />
        </ControlledTreeEnvironment>
      </div>
    </div>
  );
};

export default TraceTreeViewer;