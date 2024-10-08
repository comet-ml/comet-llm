const BASE_URL = import.meta.env.VITE_BASE_COMET_URL || "/";
const FROM_PARAM = "?from=llm";

export const buildUrl = (
  path: string,
  workspaceName?: string,
  search: string = "",
) => {
  const workspaceNameParameter = workspaceName
    ? `&from_workspace_name=${workspaceName}`
    : "";

  return `${BASE_URL}${path}${FROM_PARAM}${workspaceNameParameter}${search}`;
};

export const loadScript = (url: string) => {
  return new Promise<void>((resolve, reject) => {
    const script = document.createElement("script");
    script.src = url;
    script.async = true;
    script.addEventListener("load", () => {
      resolve();
    });
    script.addEventListener("error", () => {
      reject(new Error(`Failed to load script: ${url}`));
    });
    document.body.appendChild(script);
  });
};
