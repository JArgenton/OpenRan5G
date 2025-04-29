import { createBrowserRouter } from "react-router-dom";
import MainMenu from "./pages/MainMenu";
import RunTestTemplate from "./pages/RunTestTemplate";
import TestSelector from "./pages/TestSelector";



const router = createBrowserRouter([
    {
        path: "/",
        element: <MainMenu />
    },{
        path: "/run",
        element: <RunTestTemplate />,
        children:[
            {
                index: true,
                element: <TestSelector />
            }
        ]
    }
])

export default router