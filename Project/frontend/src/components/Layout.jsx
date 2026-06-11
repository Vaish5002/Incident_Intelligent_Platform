import React, { useState } from 'react';
import { Outlet } from 'react-router-dom';
import Sidebar from './Sidebar';
import Navbar from './Navbar';

const Layout = () => {
  const [sidebarOpen, setSidebarOpen] = useState(false);

  const toggleSidebar = () => {
    setSidebarOpen(!sidebarOpen);
  };

  return (
    <div className="min-h-screen bg-bg-darker text-gray-200">
      
      {/* Background Glowing Highlights for Premium SaaS Look */}
      <div className="absolute top-0 right-0 w-[45rem] h-[45rem] rounded-full bg-indigo-900/10 blur-[120px] pointer-events-none -z-10 animate-glow" />
      <div className="absolute bottom-20 left-10 w-[30rem] h-[30rem] rounded-full bg-violet-950/10 blur-[100px] pointer-events-none -z-10 animate-pulse-slow" />
      
      {/* Sidebar Component */}
      <Sidebar isOpen={sidebarOpen} toggleSidebar={toggleSidebar} />

      {/* Main Container */}
      <div className="flex flex-col min-h-screen md:pl-64">
        
        {/* Navbar Component */}
        <Navbar onMenuClick={toggleSidebar} />

        {/* Content Area */}
        <main className="flex-1 p-6 overflow-y-auto">
          <div className="mx-auto max-w-7xl">
            <Outlet />
          </div>
        </main>
      </div>
    </div>
  );
};

export default Layout;
