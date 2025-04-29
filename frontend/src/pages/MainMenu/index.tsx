import MenuButton from "../../Components/MenuButton"
import style from "./style.module.css"

export default function MainMenu(){
    return(
        <>
            <section className={style.wrapper}>
                <h1 className={style.title}>Network Tester</h1>
                <div className={style.container}>
                    <MenuButton text="Run test" path="/run"/>
                    <MenuButton text="Statistics" path=""/>
                    <MenuButton text="Log" path=""/>
                </div>
            </section>
        </>
    )
}