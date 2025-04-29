import { useState } from "react";
import styles from "./style.module.css";

interface ToggleButtonProps {
  label: string;
  onToggle: (label: string, active: boolean) => void;
}

export default function ToggleButton({ label, onToggle }: ToggleButtonProps) {
  const [active, setActive] = useState(false);

  const toggle = () => {
    const newState = !active;
    setActive(newState);
    onToggle(label, newState); // avisa o pai o novo estado
  };

  return (
    <button
      onClick={toggle}
      className={`${styles.button} ${active ? styles.active : ""}`}
    >
      {label}
    </button>
  );
}