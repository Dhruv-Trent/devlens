import Link from "next/link";

export default function HomePage() {
  return (
    <main className="min-h-screen flex items-center justify-center p-6">
      <div className="space-y-4 text-center">
        <h1 className="text-4xl font-bold">DevLens</h1>
        <p>Your personal AI software engineer for understanding codebases.</p>

        <div className="flex gap-4 justify-center">
          <Link
            href="/login"
            className="rounded bg-black text-white px-4 py-2"
          >
            Login
          </Link>
          <Link
            href="/register"
            className="rounded border px-4 py-2"
          >
            Register
          </Link>
        </div>
      </div>
    </main>
  );
}