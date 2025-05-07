import MenuButton from "../../Components/MenuButton"
import style from "./style.module.css"
import BackButton from "../../Components/BackButton";

export default function ClientMenu(){
    return(
        <>
            <header>
                <BackButton />
            </header>
            <section className={style.wrapper}>
                <h1 className={style.title}>Client Menu</h1>
                <div className={style.container}>
                    <MenuButton text="Run test" path="/run"/>
                    <MenuButton text="Statistics" path="/stats"/>
                    <MenuButton text="Log" path="/log"/>
                    <MenuButton text="Routine" path="/routine"/>
                </div>
            </section>
        </>
    )
}