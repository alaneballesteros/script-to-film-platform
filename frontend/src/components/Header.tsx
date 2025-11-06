import React from 'react';
import { FaFilm } from 'react-icons/fa';

const Header: React.FC = () => {
  return (
    <header className="bg-white shadow-sm border-b border-gray-200">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-3">
            <FaFilm className="text-primary-600 text-3xl" />
            <div>
              <h1 className="text-2xl font-bold text-gray-900">Script to Film</h1>
              <p className="text-sm text-gray-500">AI-Powered Short Film Creation</p>
            </div>
          </div>
          <div className="flex items-center space-x-4">
            <button className="text-gray-600 hover:text-gray-900 transition-colors">
              About
            </button>
            <button className="text-gray-600 hover:text-gray-900 transition-colors">
              Help
            </button>
          </div>
        </div>
      </div>
    </header>
  );
};

export default Header;
