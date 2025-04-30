import { useState } from "react";
import styles from "./style.module.css";

interface ToggleButtonProps {
  label: string;
  onToggle: (label: string, active: boolean) => void;
  active?: boolean;
  setActive?: (value: boolean) => void;
}

export default function ToggleButton({ label, onToggle, active: externalActive, setActive: externalSetActive }: ToggleButtonProps) {
  // estado interno, usado se props não vierem
  const [internalActive, setInternalActive] = useState(false);

  // decide qual estado usar
  const active = externalActive !== undefined ? externalActive : internalActive;
  const setActive = externalSetActive || setInternalActive;

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