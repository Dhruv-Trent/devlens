type Props = {
    label?: string;
  };
  
  export default function LoadingState({ label = "Loading..." }: Props) {
    return (
      <div className="rounded-xl border bg-white p-6 text-sm text-gray-500">
        {label}
      </div>
    );
  }