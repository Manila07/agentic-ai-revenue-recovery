import { Link } from "react-router-dom";

export default function NotFound() {
  return (
    <div className="flex items-center justify-center h-full">
      <div className="text-center">
        <p className="text-6xl mb-4">🤖</p>
        <h1 className="text-4xl font-bold text-white mb-2">404</h1>
        <p className="text-gray-400 mb-6">Page not found</p>
        <Link
          to="/"
          className="px-6 py-2 bg-blue-600 hover:bg-blue-500 text-white rounded font-bold"
        >
          Back to Dashboard
        </Link>
      </div>
    </div>
  );
}
