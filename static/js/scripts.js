document.addEventListener('DOMContentLoaded', function() {
    function fetchStatus() {
        fetch('/status')
            .then(response => response.json())
            .then(data => {
                const statusContainer = document.getElementById('status');
                statusContainer.innerHTML = '';

                data.forEach(item => {
                    const statusItem = document.createElement('div');
                    statusItem.className = item.online ? 'online' : 'offline';
                    statusItem.innerHTML = `IP: ${item.ip}, Endpoint: ${item.endpoint}, ISP: ${item.isp}, Status: ${item.online ? 'Online' : 'Offline'}`;
                    statusContainer.appendChild(statusItem);
                });
            })
            .catch(error => console.error('Error fetching status:', error));
    }

    fetchStatus();
    setInterval(fetchStatus, 5000); // updates data every 5 seconds
});