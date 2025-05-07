import BackButton from "../BackButton";

interface DHprops{
    title: String;
}

export default function DefaultHeader({title}: DHprops){
    return(
        <>
            <header>
                <BackButton />
                <h1 style ={{textAlign: "center"}}>{title}</h1>
                <hr />
            </header>
        </>
    )
}