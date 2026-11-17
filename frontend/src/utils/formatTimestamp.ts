// Formats an ISO 8601 timestamp in the user's local time.
// Older messages used "DD-MM-YYYY HH:MM AM" strings; those are shown as-is.
export function formatTimestamp(value?: string): string {
  if (!value) return "";
  const date = new Date(value);
  if (Number.isNaN(date.getTime()) || !value.includes("T")) return value;
  return date.toLocaleString(undefined, {
    day: "2-digit",
    month: "short",
    hour: "2-digit",
    minute: "2-digit",
  });
}
