import { Link } from "react-router-dom"
import style from "./style.module.css"

interface MenuButtonProps{
    text: string,
    path: string
}

export default function MenuButton({text, path}: MenuButtonProps){
    return(
        <Link to={path}><button className={style.btn}>{text}</button></Link>
    )
}