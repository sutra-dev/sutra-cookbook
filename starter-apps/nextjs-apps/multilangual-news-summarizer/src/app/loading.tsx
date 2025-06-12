export default function Loading() {
  return (
    <div className="flex justify-center items-center min-h-screen">
      <div className="text-center">
        <div className="inline-block animate-spin rounded-full h-12 w-12 border-4 border-solid border-blue-600 border-r-transparent" role="status">
          <span className="sr-only">Loading...</span>
        </div>
        <h2 className="mt-4 text-xl font-semibold">Loading</h2>
        <p className="text-sm text-gray-500 dark:text-gray-400">Please wait while we process your request</p>
      </div>
    </div>
  );
} 