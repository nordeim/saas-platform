'use client';

import { useState } from 'react';
import { ArrowRightIcon, PlayIcon } from '@heroicons/react/24/solid';

export default function HeroSection() {
  const [isHovered, setIsHovered] = useState(false);

  return (
    <section className="relative min-h-screen flex items-center justify-center overflow-hidden">
      {/* Background gradient */}
      <div className="absolute inset-0 bg-gradient-to-br from-primary-50 via-white to-singapore-blue/10"></div>
      
      {/* Animated background elements */}
      <div className="absolute inset-0">
        <div className="absolute top-1/4 left-1/4 w-96 h-96 bg-primary-200/20 rounded-full blur-3xl animate-pulse"></div>
        <div className="absolute bottom-1/4 right-1/4 w-96 h-96 bg-singapore-red/20 rounded-full blur-3xl animate-pulse delay-1000"></div>
      </div>

      <div className="relative z-10 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 items-center">
          {/* Left side - Text content */}
          <div className="text-center lg:text-left">
            <div className="mb-6">
              <span className="inline-flex items-center px-4 py-2 rounded-full text-sm font-medium bg-singapore-red/10 text-singapore-red border border-singapore-red/20">
                🇸🇬 Singapore B2B SaaS Platform
              </span>
            </div>

            <h1 className="text-5xl md:text-6xl lg:text-7xl font-bold text-gray-900 mb-6">
              <span className="bg-gradient-to-r from-primary-600 to-singapore-red bg-clip-text text-transparent">
                NexusCore
              </span>
              <br />
              <span className="text-gray-900">
                Professional SaaS
              </span>
            </h1>

            <p className="text-xl md:text-2xl text-gray-600 mb-8 leading-relaxed">
              Built for Singapore businesses with GST compliance, 
              PDPA automation, and enterprise-grade security.
            </p>

            <div className="flex flex-col sm:flex-row gap-4 justify-center lg:justify-start">
              <button
                className="group inline-flex items-center justify-center px-8 py-4 text-lg font-semibold text-white bg-singapore-red rounded-xl hover:bg-singapore-red/90 transition-all duration-300 transform hover:scale-105 shadow-lg hover:shadow-xl"
                onMouseEnter={() => setIsHovered(true)}
                onMouseLeave={() => setIsHovered(false)}
              >
                Start Free Trial
                <ArrowRightIcon className={`ml-2 h-5 w-5 transition-transform duration-300 ${isHovered ? 'translate-x-1' : ''}`} />
              </button>

              <button className="inline-flex items-center justify-center px-8 py-4 text-lg font-semibold text-gray-700 bg-white rounded-xl border-2 border-gray-200 hover:border-gray-300 transition-all duration-300 shadow-sm hover:shadow-md">
                <PlayIcon className="mr-2 h-5 w-5" />
                Watch Demo
              </button>
            </div>

            <div className="mt-12 flex flex-wrap items-center justify-center lg:justify-start gap-8 text-sm text-gray-500">
              <div className="flex items-center">
                <span className="w-2 h-2 bg-green-500 rounded-full mr-2"></span>
                GST Compliant
              </div>
              <div className="flex items-center">
                <span className="w-2 h-2 bg-green-500 rounded-full mr-2"></span>
                PDPA Automated
              </div>
              <div className="flex items-center">
                <span className="w-2 h-2 bg-green-500 rounded-full mr-2"></span>
                99.9% Uptime
              </div>
            </div>
          </div>

          {/* Right side - Visual element */}
          <div className="relative">
            <div className="relative glass p-8 rounded-2xl shadow-elementra">
              <div className="space-y-4">
                {/* Mock dashboard preview */}
                <div className="flex items-center justify-between">
                  <div className="h-4 w-32 bg-gray-200 rounded animate-pulse"></div>
                  <div className="h-4 w-16 bg-singapore-red/20 rounded"></div>
                </div>
                
                <div className="space-y-3">
                  {[1, 2, 3].map((i) => (
                    <div key={i} className="flex items-center space-x-4">
                      <div className="h-10 w-10 bg-primary-100 rounded-lg flex items-center justify-center">
                        <div className="h-6 w-6 bg-primary-500 rounded"></div>
                      </div>
                      <div className="flex-1">
                        <div className="h-3 bg-gray-200 rounded w-3/4 mb-1"></div>
                        <div className="h-2 bg-gray-100 rounded w-1/2"></div>
                      </div>
                      <div className="h-6 w-16 bg-gray-200 rounded"></div>
                    </div>
                  ))}
                </div>

                <div className="pt-4 border-t border-gray-200">
                  <div className="flex items-center justify-between text-sm">
                    <span className="text-gray-500">Total Revenue</span>
                    <span className="font-semibold text-singapore-red">$125,430.00</span>
                  </div>
                  <div className="flex items-center justify-between text-sm mt-1">
                    <span className="text-gray-500">GST (9%)</span>
                    <span className="font-semibold">$11,288.70</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}