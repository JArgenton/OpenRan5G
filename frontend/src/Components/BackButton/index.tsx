import { useNavigate } from "react-router-dom";
import style from "./style.module.css";

export default function BackButton() {
  const navigate = useNavigate();

  return (
    <button className={style.backBtn} onClick={() => navigate(-1)}>
      ← Voltar
    </button>
  );
}