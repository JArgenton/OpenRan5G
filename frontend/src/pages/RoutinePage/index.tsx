import DefaultHeader from "../../Components/DefaultHeader";
import MenuButton from "../../Components/MenuButton";



export default function RoutinePage(){

    return(
        <>
            <DefaultHeader title="Routine" />
            <div style={{ display: "flex", justifyContent: "center", gap: "2rem", marginTop: "2rem" }}>
                <MenuButton text="Add new routine" path="/addr" />
                <MenuButton text="Get saved routines" path="/saved" />
            </div>
        </>
    )
}