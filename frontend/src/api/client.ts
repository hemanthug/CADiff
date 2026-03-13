export type CompareResponse = {
  status: "ok" | "error";
  report?: any;
  error?: string;
};

const API_BASE = "http://localhost:8000";

export async function compareParts(fileA: File, fileB: File, tolerance: number): Promise<CompareResponse> {
  const formData = new FormData();
  formData.append("file_a", fileA);
  formData.append("file_b", fileB);
  formData.append("tolerance", tolerance.toString());

  const response = await fetch(`${API_BASE}/compare`, {
    method: "POST",
    body: formData,
  });

  return response.json();
}
