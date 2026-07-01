import { ReactNode } from "react";
import Card from "./Card";

type Props = {
  title: string;
  description?: string;
  children: ReactNode;
};

export default function Section({
  title,
  description,
  children,
}: Props) {
  return (
    <Card className="p-4 space-y-4">
      <div>
        <h2 className="text-xl font-semibold">{title}</h2>

        {description && (
          <p className="text-sm text-gray-500">{description}</p>
        )}
      </div>

      {children}
    </Card>
  );
}