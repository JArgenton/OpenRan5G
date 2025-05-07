import TestForm from "../../Components/TestForm";
import DefaultHeader from "../../Components/DefaultHeader";


export default function TestSelector() {
  
  function handleSubmit(parameters: string[], protocol: boolean[]){
    console.log(parameters, protocol)
  }

  return (
    <>
      <DefaultHeader title="Run Test" />
      <div style={{ display: 'flex', justifyContent: 'center', padding: '2rem' }}>
        <TestForm onSubmit={handleSubmit} />
      </div>
    </>
  )
}