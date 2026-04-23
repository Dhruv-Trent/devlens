"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { getToken, removeToken } from "@/lib/auth";

type User = {
  id: number;
  name: string;
  email: string;
};

export default function DashboardPage() {
  const router = useRouter();
  const [user, setUser] = useState<User | null>(null);

  useEffect(() => {
    const token = getToken();

    if (!token) {
      router.push("/login");
      return;
    }

    async function fetchMe() {
      try {
        const res = await fetch(
          `${process.env.NEXT_PUBLIC_API_URL}/auth/me`,
          {
            headers: {
              Authorization: `Bearer ${token}`,
            },
          }
        );

        if (!res.ok) {
          removeToken();
          router.push("/login");
          return;
        }

        const data = await res.json();
        setUser(data);
      } catch {
        removeToken();
        router.push("/login");
      }
    }

    fetchMe();
  }, [router]);

  function handleLogout() {
    removeToken();
    router.push("/login");
  }

  if (!user) {
    return <main className="p-6">Loading dashboard...</main>;
  }

  return (
    <main className="min-h-screen p-6">
      <div className="max-w-4xl mx-auto space-y-4">
        <h1 className="text-3xl font-bold">Dashboard</h1>
        <p>Welcome, {user.name}</p>
        <p>Email: {user.email}</p>

        <button
          onClick={handleLogout}
          className="rounded bg-red-600 text-white px-4 py-2"
        >
          Logout
        </button>
      </div>
    </main>
  );
}