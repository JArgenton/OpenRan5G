import { useState } from "react"
import DefaultHeader from "../../Components/DefaultHeader"
import style from "./style.module.css"
import DefaultButton from "../../Components/DefaultButton"

export default function ServerMenu() {
  const [server, setServer] = useState<boolean>(false)

  function handleTestButton() {
    const newState = !server
    setServer(newState)
    // chamar API real
  }

  return (
    <>
      <DefaultHeader title="Server Menu" />
      <div className={style.wrapper}>
        <div className={style.statusSection}>
          <span className={style.statusText}>
            Server status: 
            <span className={server ? style.statusOn : style.statusOff}>
              {server ? " On" : " Off"}
            </span>
          </span>
          <DefaultButton text={`${server ? "Stop" : "Start"} server`} callback={handleTestButton} />
        </div>
      </div>
    </>
  )
}