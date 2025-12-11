import { BrowserRouter, Routes, Route } from "react-router-dom";
import Home from "./pages/Home";
import Login from "./pages/Login";
import Register from "./pages/Register";
import ProtectedRoute from "./ProtectedRoute";
import Logout from "./pages/Logout"; 
import AddInvestment from "./components/AddInvestment";
import RecentInvestments from "./components/RecentInvestments";
import ViewInvestments from "./components/Viewinvestments";
import PredictStock from "./components/PredictStock";
import Analytics from "./components/Analytics";
export default function AppRouter() {
  return (
    <BrowserRouter>
      <Routes>
        <Route 
          path="/home" 
          element={
            <ProtectedRoute>
              <Home />
            </ProtectedRoute>
          }
        />
        
        <Route 
          path="/add-investment" 
          element={
            <ProtectedRoute>
              <AddInvestment />
            </ProtectedRoute>
          }
        />
         <Route 
          path="/recent-investment" 
          element={
            <ProtectedRoute>
              <RecentInvestments />
            </ProtectedRoute>
          }
        />
        <Route 
          path="/view-investments" 
          element={
            <ProtectedRoute>
             <ViewInvestments></ViewInvestments>
            </ProtectedRoute>
          }
        />
         <Route 
          path="/analytics" 
          element={
            <ProtectedRoute>
            <Analytics></Analytics>
            </ProtectedRoute>
          }
        />
     <Route 
          path="/predict-stock" 
          element={
            <ProtectedRoute>
           <PredictStock></PredictStock>
            </ProtectedRoute>
          }
        />


        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />

        {/* Create a route for Logout */}
        <Route 
          path="/logout" 
          element={<Logout />}  
        />
      </Routes>
    </BrowserRouter>
  );
}
