import { Outlet } from "react-router-dom";
import BackButton from "../../Components/BackButton";


export default function RunTestTemplate(){
    return(
        <>
            <header>
                <BackButton />
                <h1 style ={{textAlign: "center"}}>Run Tests</h1>

                <hr />
            </header>
            <section>
                <Outlet />
            </section>
        </>
    )
}