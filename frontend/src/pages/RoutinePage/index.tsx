import DefaultHeader from "../../Components/DefaultHeader";
import TestForm from "../../Components/TestForm";


export default function RoutinePage(){

    return(
        <>
            <DefaultHeader title="Routine" />

            <div style={{ display: 'flex', height: '100vh' }}>
                <section style={{ width: '50%', padding: '2rem' }}>
                    <h2 style={{ paddingLeft: "5%" }}>Add new test routine</h2>
                    <TestForm onSubmit={() => {}} />
                </section>

                <section style={{ width: '50%', padding: '2rem', borderLeft: '1px solid #444' }}>
                    <h2>Saved Routines</h2>
                    {/* Aqui você pode listar as rotinas salvas */}
                </section>
            </div>
        </>
    )
}