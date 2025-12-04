async function fetchData() {
  try {
    const response = await fetch("http://localhost:8000/");

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const data = await response.json();
    return data.message;
  } catch (error) {
    console.error("Fetch Error:", error);
    return "❌ BACKEND CONNECTION FAILED. Check server terminals.";
  }
}

export default async function Home() {
  const message = await fetchData();

  return (
    <div className="flex items-center justify-center min-h-screen bg-slate-50">
      <div className="text-2xl font-semibold p-10 bg-white shadow-xl rounded-lg">
        <h1 className="text-xl text-gray-700">Message from API:</h1>
        <p className="mt-2 text-teal-600">{message}</p>
      </div>
    </div>
  );
}
