using System;

namespace SovereignMemoryDaemon;

public class MemoryItem
{
    public string Title { get; set; } = string.Empty;
    public string Path { get; set; } = string.Empty;
    public string Content { get; set; } = string.Empty;
    public string Category { get; set; } = string.Empty;
    public DateTime LastModified { get; set; }
}
