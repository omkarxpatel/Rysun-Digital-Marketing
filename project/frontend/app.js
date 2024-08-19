const { useEffect, useState } = React;

function App() {
    const [status, setStatus] = useState("Loading...");

    useEffect(() => {
        const interval = setInterval(() => {
            fetch('http://localhost:5000/status')
                .then(response => response.json())
                .then(data => setStatus(data.message))
                .catch(error => setStatus("Error fetching status"));
        }, 5000);

        return () => clearInterval(interval);
    }, []);

    return (
        <div className="h-screen flex flex-col">
            <div className="h-1/4 bg-gray-200 p-4 border-b border-gray-400">Top Part</div>
            <div className="flex flex-1">
                <div className="w-1/4 bg-gray-100 p-4 border-r border-gray-400">Left Part</div>
                <div className="flex-1 flex flex-col">
                    <div className="flex-1 border-b border-dotted border-gray-500 p-4 border-r border-gray-400">Center Top</div>
                    <div className="flex-1 p-4 border-r border-gray-400">Center Bottom</div>
                </div>
                <div className="w-1/4 bg-gray-100 p-4">Right Part</div>
            </div>
            <div className="p-4 bg-gray-300 border-t border-gray-400">
                Server Status: {status}
            </div>
        </div>
    );
}

ReactDOM.render(<App />, document.getElementById('root'));
