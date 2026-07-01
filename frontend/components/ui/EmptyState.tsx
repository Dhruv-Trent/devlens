type Props = {
    title: string;
    description: string;
  };
  
  export default function EmptyState({ title, description }: Props) {
    return (
      <div className="rounded-xl border border-dashed bg-gray-50 p-6 text-center">
        <h3 className="font-semibold">{title}</h3>
        <p className="mt-1 text-sm text-gray-500">{description}</p>
      </div>
    );
  }