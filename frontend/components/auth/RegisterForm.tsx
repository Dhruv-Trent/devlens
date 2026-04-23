"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { apiFetch } from "@/lib/api";
import { useEffect } from "react";
import { getToken } from "@/lib/auth";

type FormData = {
  name: string;
  email: string;
  password: string;
};

type FormErrors = {
  name?: string;
  email?: string;
  password?: string;
  general?: string;
};

export default function RegisterForm() {

  const router = useRouter();
  
  useEffect(() => {
    if (getToken()) {
      router.replace("/dashboard");
    }
  }, [router]);

  const [formData, setFormData] = useState<FormData>({
    name: "",
    email: "",
    password: "",
  });

  const [error, setError] = useState("");
  const [errors, setErrors] = useState<FormErrors>({});
  const [loading, setLoading] = useState(false);

  function validate(values: FormData): FormErrors {
    const newErrors: FormErrors = {};

    if (!values.name.trim()) {
      newErrors.name = "Name is required";
    } else if (values.name.trim().length < 2) {
      newErrors.name = "Name must be at least 2 characters";
    }

    if (!values.email.trim()) {
      newErrors.email = "Email is required";
    } else if (!/^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}$/i.test(values.email)) {
      newErrors.email = "Enter a valid email address";
    }

    if (!values.password) {
      newErrors.password = "Password is required";
    } else if (values.password.length < 8) {
      newErrors.password = "Password must be at least 8 characters";
    } else if (!/(?=.*[A-Z])(?=.*[a-z])(?=.*\d)/.test(values.password)) {
      newErrors.password =
        "Password must include uppercase, lowercase, and a number";
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

    // console.log(formData)
    try {
      await apiFetch("/auth/register", {
        method: "POST",
        body: JSON.stringify(formData),
   
      });

      router.push("/login");
    } catch (err: any) {
      setError(err.message || "Registration failed");
    } finally {
      setLoading(false);
    }
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-4 max-w-md min-w-[330px]" noValidate>
      <h1 className="text-2xl font-bold">Create Account</h1>
      <div>
        <input
          type="text"
          name="name"
          placeholder="Name"
          value={formData.name}
          onChange={handleChange}
          className="w-full border rounded px-3 py-2"
        />
        <p className="text-red-500 text-sm min-h-[8px]">
          {errors.name || ""}
        </p>
      </div>
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
        {loading ? "Creating account..." : "Register"}
      </button>
    </form>
  );
}
