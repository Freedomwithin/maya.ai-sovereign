using System;
using System.Collections.Generic;
using System.Linq;
using System.IO;

namespace SovereignMemoryDaemon;

public class MemoryRepository
{
    private List<MemoryItem> _memoryCache = new List<MemoryItem>();
    private readonly string[] _targetPaths;
    public int ItemCount => _memoryCache.Count;
    public DateTime LastRefresh { get; private set; } = DateTime.MinValue;

    public MemoryRepository(string[] targetPaths)
    {
        _targetPaths = targetPaths;
    }

    public void RefreshIndex()
    {
        var newCache = new List<MemoryItem>();
        foreach (var path in _targetPaths)
        {
            if (Directory.Exists(path))
            {
                var files = Directory.GetFiles(path, "*.*", SearchOption.AllDirectories)
                    .Where(f => f.EndsWith(".md") || f.EndsWith(".json") || f.EndsWith(".py") || f.EndsWith(".sh"));

                foreach (var file in files)
                {
                    try
                    {
                        newCache.Add(new MemoryItem
                        {
                            Title = Path.GetFileName(file),
                            Path = file,
                            Category = path.Split(Path.DirectorySeparatorChar).Last(),
                            LastModified = File.GetLastWriteTime(file)
                        });
                    }
                    catch { /* Skip locked files */ }
                }
            }
        }
        _memoryCache = newCache;
        LastRefresh = DateTime.Now;
    }

    public List<MemoryItem> Search(string query)
    {
        if (string.IsNullOrWhiteSpace(query)) return new List<MemoryItem>();
        
        // Simple high-velocity fuzzy match (inspired by TerminalGen)
        return _memoryCache
            .Where(m => m.Title.Contains(query, StringComparison.OrdinalIgnoreCase) || 
                        m.Path.Contains(query, StringComparison.OrdinalIgnoreCase))
            .OrderByDescending(m => m.LastModified)
            .Take(10)
            .ToList();
    }
}
