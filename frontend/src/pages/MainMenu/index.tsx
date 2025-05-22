import MenuButton from "../../Components/MenuButton"
import style from "./style.module.css"

export default function MainMenu(){
    return(
        <>
            <section className={style.wrapper}>
                <h1 className={style.title}>Network Tester</h1>
                <div className={style.container}>
                    <MenuButton text="Client" path="/client"/>
                    <MenuButton text="Server" path="/server"/>
                </div>
            </section>
        </>
    )
}