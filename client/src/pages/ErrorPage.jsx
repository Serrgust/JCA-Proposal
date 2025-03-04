import { useRouteError } from "react-router-dom";

function ErrorPage() {
  const error = useRouteError();

  return (
    <div className="text-center">
      <h1 className="text-4xl font-bold text-red-500">Oops!</h1>
      <p>Something went wrong:</p>
      <pre>{error.statusText || error.message}</pre>
    </div>
  );
}

export default ErrorPage; // ✅ Make sure this is a default export
