"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { apiFetch } from "@/lib/api";
import { saveToken } from "@/lib/auth";
import { useEffect } from "react";
import { getToken } from "@/lib/auth";

type FormErrors = {
  email?: string;
  password?: string;
};

export default function LoginForm() {
  const router = useRouter();

  const [formData, setFormData] = useState({
    email: "",
    password: "",
  });

  useEffect(() => {
    if (getToken()) {
      router.replace("/dashboard");
    }
  }, [router]);

  const [error, setError] = useState("");
  const [errors, setErrors] = useState<FormErrors>({});
  const [loading, setLoading] = useState(false);

  function validate(values: typeof formData): FormErrors {
    const newErrors: FormErrors = {};

    if (!values.email.trim()) {
      newErrors.email = "Email is required";
    } else if (!/^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}$/i.test(values.email)) {
      newErrors.email = "Enter a valid email";
    }

    if (!values.password) {
      newErrors.password = "Password is required";
    }

    return newErrors;
  }

  function handleChange(e: React.ChangeEvent<HTMLInputElement>) {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
  }

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();

    const validationErrors = validate(formData);
    if (Object.keys(validationErrors).length > 0) {
      setErrors(validationErrors);
      return;
    }

    setErrors({});
    setError("");
    setLoading(true);

    try {
      const data = await apiFetch("/auth/login", {
        method: "POST",
        body: JSON.stringify(formData),
      });

      saveToken(data.access_token);
      router.replace("/dashboard");
    } catch (err: any) {
      setError(err.message || "Login failed");
    } finally {
      setLoading(false);
    }
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-4 max-w-md min-w-[330px]" noValidate>
      <h1 className="text-2xl font-bold">Login</h1>
      <div>
        <input
          type="email"
          name="email"
          placeholder="Email"
          value={formData.email}
          onChange={handleChange}
          className="w-full border rounded px-3 py-2"
        />
        <p className="text-red-500 text-sm min-h-[8px]">
          {errors.email || ""}
        </p>
      </div>

      <div>
        <input
          type="password"
          name="password"
          placeholder="Password"
          value={formData.password}
          onChange={handleChange}
          className="w-full border rounded px-3 py-2"
        />
        <p className="text-red-500 text-sm min-h-[8px]">
          {errors.password || ""}
        </p>
      </div>

      {error && <p className="text-red-500 text-sm">{error}</p>}


      <button
        type="submit"
        disabled={loading}
        className="w-full rounded bg-black text-white py-2"
      >
        {loading ? "Logging in..." : "Login"}
      </button>
    </form>
  );
}
