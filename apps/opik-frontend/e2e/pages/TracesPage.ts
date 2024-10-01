import { Locator, Page } from "@playwright/test";
import { SidePanel } from "@e2e/pages/components/SidePanel";
import { Table } from "@e2e/pages/components/Table";
import { Columns } from "@e2e/pages/components/Columns";

export class TracesPage {
  readonly sidebarScores: Locator;
  readonly tableScores: Locator;
  readonly title: Locator;

  readonly columns: Columns;
  readonly sidePanel: SidePanel;
  readonly table: Table;

  constructor(readonly page: Page) {
    this.tableScores = page.getByTestId("feedback-score-tag");
    this.sidebarScores = page.getByLabel("Feedback Scores");
    this.title = page.getByRole("heading", { name: "Traces" });

    this.columns = new Columns(page);
    this.sidePanel = new SidePanel(page, "traces");
    this.table = new Table(page);
  }

  async goto(projectId: string) {
    await this.page.goto(`/default/projects/${projectId}/traces`);
  }

  async openSidePanel(name: string) {
    await this.table.getRowLocatorByCellText(name).click();
  }

  async clearScore(name: string) {
    await this.page
      .getByRole("row", { name: `ui ${name}` })
      .getByRole("button")
      .click();
    await this.page
      .getByRole("button", { name: "Clear feedback score" })
      .click();
  }

  getScoreValueCell(name: string) {
    return this.page.locator(`[data-test-value="${name}"]`).first();
  }

  getScoreValue(name: string) {
    return this.tableScores
      .filter({
        has: this.page.getByTestId("feedback-score-tag-label").getByText(name),
      })
      .first()
      .getByTestId("feedback-score-tag-value");
  }

  async openAnnotate() {
    await this.page.getByRole("button", { name: "Annotate" }).click();
  }

  async closeAnnotate() {
    await this.page.getByRole("button", { name: "Close" }).click();
  }

  async selectSidebarTab(name: string) {
    await this.sidePanel.container.getByRole("tab", { name }).click();
  }

  async setCategoricalScore(name: string, categoryName: string) {
    await this.getScoreValueCell(name)
      .getByRole("radio", { name: categoryName })
      .click();
  }

  async setNumericalScore(name: string, value: number) {
    await this.getScoreValueCell(name).locator("input").fill(String(value));
  }

  async switchToLLMCalls() {
    await this.page.getByText("LLM calls").click();
  }

  async addTag(tag: string) {
    await this.page.getByTestId("add-tag-button").click();
    await this.page.getByPlaceholder("New tag").fill(tag);
    await this.page.getByRole("button", { name: "Add tag" }).click();
  }

  async deleteTag(tag: string) {
    await this.sidePanel.container.getByText(tag).hover();
    await this.sidePanel.container.getByText(tag).locator("../button").click();
  }
}
