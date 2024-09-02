import React, { useMemo, useState } from "react";
import { Check, Plus } from "lucide-react";
import sortBy from "lodash/sortBy";

import { Button } from "@/components/ui/button";
import {
  Popover,
  PopoverContent,
  PopoverTrigger,
} from "@/components/ui/popover";
import { TraceFeedbackScore } from "@/types/traces";
import useTraceFeedbackScoreSetMutation from "@/api/traces/useTraceFeedbackScoreSetMutation";
import useAppStore from "@/store/AppStore";
import useFeedbackDefinitionsList from "@/api/feedback-definitions/useFeedbackDefinitionsList";
import {
  FEEDBACK_DEFINITION_TYPE,
  FeedbackDefinition,
} from "@/types/feedback-definitions";
import SearchInput from "@/components/shared/SearchInput/SearchInput";
import ColoredTag from "@/components/shared/ColoredTag/ColoredTag";
import { toLower } from "lodash";
import { Input } from "@/components/ui/input";
import { ToggleGroup, ToggleGroupItem } from "@/components/ui/toggle-group";
import { isNumericFeedbackScoreValid } from "@/lib/traces";

type AddFeedbackScorePopoverProps = {
  feedbackScores: TraceFeedbackScore[];
  traceId: string;
  spanId?: string;
};

const AddFeedbackScorePopover: React.FunctionComponent<
  AddFeedbackScorePopoverProps
> = ({ feedbackScores = [], traceId, spanId }) => {
  const [open, setOpen] = useState(false);
  const [search, setSearch] = useState("");

  const [activeFeedbackDefinition, setActiveFeedbackDefinition] =
    useState<FeedbackDefinition>();
  const [value, setValue] = useState<number>();

  const workspaceName = useAppStore((state) => state.activeWorkspaceName);
  const { data: feedbackDefinitionsData } = useFeedbackDefinitionsList({
    workspaceName,
    page: 1,
    size: 1000,
  });

  const isNumericValid =
    activeFeedbackDefinition?.type === FEEDBACK_DEFINITION_TYPE.numerical &&
    isNumericFeedbackScoreValid(activeFeedbackDefinition?.details, value);

  const resetState = () => {
    setSearch("");
    setActiveFeedbackDefinition(undefined);
    setValue(undefined);
  };

  const feedbackDefinitions: FeedbackDefinition[] = useMemo(
    () =>
      sortBy(
        (feedbackDefinitionsData?.content || []).filter(
          (feedbackDefinition) => {
            return (
              (search
                ? toLower(feedbackDefinition.name).includes(toLower(search))
                : true) &&
              !feedbackScores.find(
                (feedbackScore) =>
                  feedbackScore.name === feedbackDefinition.name,
              )
            );
          },
        ),
        "name",
      ),
    [feedbackDefinitionsData?.content, feedbackScores, search],
  );

  const setTraceFeedbackScoreMutation = useTraceFeedbackScoreSetMutation();

  const handleAddFeedbackScore = (value: number, categoryName?: string) => {
    if (!activeFeedbackDefinition) return;

    setTraceFeedbackScoreMutation.mutate({
      categoryName,
      name: activeFeedbackDefinition.name,
      spanId,
      traceId,
      value,
    });
    setOpen(false);
  };

  const renderSearchContent = () => {
    return (
      <div className="w-52">
        <SearchInput
          searchText={search}
          setSearchText={setSearch}
        ></SearchInput>
        <div className="mt-4 max-h-[400px] overflow-y-auto">
          {feedbackDefinitions.length === 0 && (
            <div className="flex items-center justify-center py-6 text-muted-slate">
              No results
            </div>
          )}

          {feedbackDefinitions.map((feedbackDefinition) => (
            <div
              key={feedbackDefinition.name}
              className="flex h-10 cursor-pointer items-center"
              onClick={() => setActiveFeedbackDefinition(feedbackDefinition)}
            >
              <ColoredTag label={feedbackDefinition.name} />
            </div>
          ))}
        </div>
      </div>
    );
  };

  const renderOptions = () => {
    if (!activeFeedbackDefinition) return null;

    if (activeFeedbackDefinition.type === FEEDBACK_DEFINITION_TYPE.numerical) {
      return (
        <div className="w-full">
          <div className="flex gap-2">
            <div className="flex-auto">
              <Input
                max={activeFeedbackDefinition.details.max}
                min={activeFeedbackDefinition.details.min}
                onChange={(event) => setValue(Number(event.target.value))}
                placeholder="Value"
                type="number"
                value={String(value)}
              />
            </div>
            <div>
              <Button
                size="icon"
                disabled={!isNumericValid}
                onClick={() => {
                  if (isNumericValid) {
                    handleAddFeedbackScore(value as number);
                  }
                }}
              >
                <Check className="size-4" />
              </Button>
            </div>
          </div>
          <div className="comet-body-s mt-1 truncate text-light-slate">
            Value range {activeFeedbackDefinition.details.min}-
            {activeFeedbackDefinition.details.max}
          </div>
        </div>
      );
    }

    if (
      activeFeedbackDefinition.type === FEEDBACK_DEFINITION_TYPE.categorical
    ) {
      return (
        <div className="w-full overflow-x-auto">
          <ToggleGroup
            className="w-fit"
            onValueChange={(newCategoryName) => {
              const categoryEntry = Object.entries(
                activeFeedbackDefinition.details.categories,
              ).find(([categoryName]) => categoryName === newCategoryName);

              if (categoryEntry) {
                handleAddFeedbackScore(categoryEntry[1], newCategoryName);
              }
            }}
            type="single"
          >
            {Object.entries(activeFeedbackDefinition.details.categories).map(
              ([categoryName, categoryValue]) => {
                return (
                  <ToggleGroupItem key={categoryName} value={categoryName}>
                    <div className="text-nowrap">
                      {categoryName} ({categoryValue})
                    </div>
                  </ToggleGroupItem>
                );
              },
            )}
          </ToggleGroup>
        </div>
      );
    }

    return null;
  };

  const renderEditContent = () => {
    return (
      <div className="min-w-52 max-w-[40vw]">
        <div className="comet-body-s-accented mb-1.5 truncate">
          {activeFeedbackDefinition?.name}
        </div>
        <div className="flex w-full">{renderOptions()}</div>
      </div>
    );
  };

  return (
    <Popover
      onOpenChange={(state) => {
        setOpen(state);
        if (state) {
          resetState();
        }
      }}
      open={open}
    >
      <PopoverTrigger asChild>
        <Button variant="outline" size="icon-sm" className="size-7">
          <Plus className="size-4" />
        </Button>
      </PopoverTrigger>
      <PopoverContent className="p-4" align="end">
        {activeFeedbackDefinition ? renderEditContent() : renderSearchContent()}
      </PopoverContent>
    </Popover>
  );
};

export default AddFeedbackScorePopover;