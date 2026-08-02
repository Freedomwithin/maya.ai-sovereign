using System.Net;
using System.Net.Sockets;
using System.Text;
using Newtonsoft.Json;

namespace SovereignMemoryDaemon;

public class Worker : BackgroundService
{
    private readonly ILogger<Worker> _logger;
    private readonly MemoryRepository _repository;
    private readonly string[] _targetPaths = {
        "/home/jonathon/gemini-jules/maya/memories",
        "/home/jonathon/gemini-jules/maya/VAULT",
        "/home/jonathon/gemini-jules/maya/projects",
        "/home/jonathon/gemini-jules/maya/documents",
        "/home/jonathon/gemini-jules/maya/scripts"
    };

    public Worker(ILogger<Worker> logger)
    {
        _logger = logger;
        _repository = new MemoryRepository(_targetPaths);
    }

    protected override async Task ExecuteAsync(CancellationToken stoppingToken)
    {
        _logger.LogInformation("Sovereign Memory Daemon starting at: {time}", DateTimeOffset.Now);
        
        // Initial Indexing
        _repository.RefreshIndex();
        
        // Start TCP Listener for Python IPC
        var listener = new TcpListener(IPAddress.Loopback, 5555);
        listener.Start();
        _logger.LogInformation("Sovereign Socket active on port 5555.");

        while (!stoppingToken.IsCancellationRequested)
        {
            if (listener.Pending())
            {
                using var client = await listener.AcceptTcpClientAsync();
                using var stream = client.GetStream();
                var buffer = new byte[1024];
                var bytesRead = await stream.ReadAsync(buffer, 0, buffer.Length);
                var query = Encoding.UTF8.GetString(buffer, 0, bytesRead).Trim();
                
                _logger.LogInformation("Memory Request received: {query}", query);
                
                if (query == "REFRESH") {
                    _repository.RefreshIndex();
                    var success = Encoding.UTF8.GetBytes("Index Refreshed.");
                    await stream.WriteAsync(success, 0, success.Length);
                } else if (query == "STATS") {
                    var stats = new {
                        Count = _repository.ItemCount,
                        LastRefresh = _repository.LastRefresh,
                        Status = "Online",
                        Protocol = "Sovereign_v2.1"
                    };
                    var json = JsonConvert.SerializeObject(stats);
                    var data = Encoding.UTF8.GetBytes(json);
                    await stream.WriteAsync(data, 0, data.Length);
                } else {
                    var results = _repository.Search(query);
                    var json = JsonConvert.SerializeObject(results);
                    var data = Encoding.UTF8.GetBytes(json);
                    await stream.WriteAsync(data, 0, data.Length);
                }
            }

            // Periodic Refresh every 15 mins
            if (DateTime.Now.Minute % 15 == 0 && DateTime.Now.Second < 5)
            {
                _repository.RefreshIndex();
            }

            await Task.Delay(100, stoppingToken);
        }
        listener.Stop();
    }
}
