import style from "./style.module.css"

interface DBprops{
    text: string,
    callback: () => void
}

export default function DefaultButton({text, callback}: DBprops){
    return(
        <button onClick={callback} className={style.btn}>{text}</button>
    )
}