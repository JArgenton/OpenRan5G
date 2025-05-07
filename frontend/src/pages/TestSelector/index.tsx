import TestForm, { Test } from "../../Components/TestForm";
import DefaultHeader from "../../Components/DefaultHeader";


export default function TestSelector() {
  
  function handleSubmit(test: Test[]){
    console.log(test)
  }

  return (
    <>
      <DefaultHeader title="Run Test" />
      <div style={{ display: 'flex', justifyContent: 'center', padding: '2rem' }}>
        <TestForm onSubmit={handleSubmit} text="Run tests"/>
      </div>
    </>
  )
}