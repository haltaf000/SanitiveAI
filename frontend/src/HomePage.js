import React, { useEffect } from 'react';
import './App.css';

const HomePage = () => {
  useEffect(() => {
    const mission = document.querySelector('.mission');
    const navbarHeight = document.querySelector('.header').offsetHeight;

    const handleScroll = () => {
      const missionTop = mission.getBoundingClientRect().top;
      const missionBottom = mission.getBoundingClientRect().bottom;

      if (missionTop <= navbarHeight && missionBottom >= navbarHeight) {
        mission.classList.add('focused');
      } else {
        mission.classList.remove('focused');
      }
    };

    window.addEventListener('scroll', handleScroll);
    return () => {
      window.removeEventListener('scroll', handleScroll);
    };
  }, []);
return (
    <div className="homepage">
      <section className="hero">
        <h1>Environmental Responsibility Made Profitable</h1>
        <p>SanitiveAi is an innovative technology company that 
          empowers businesses across industries to reduce their 
          environmental impact and drive sustainability through 
          advanced analytics and machine learning. Our data-driven 
          approach enables businesses to make informed decisions and
           achieve their environmental goals while also improving 
           profitability.</p>
      </section>
      <div id="contentWrapper">
      <section className="mission">
        <h2>ADVANCED ANALYTICS FOR SUSTAINABLE BUSINESS GROWTH</h2>
        <p>
        Transform your business with SanitiveAI's data-driven sustainability solutions. 
        Reduce your environmental impact, cut costs, and enhance profitability. Join us in 
        creating a healthier planet and a more sustainable future for your business.
        </p>
      </section>
      </div>
      <section className="services">
      <h1>Our Specialized Industries</h1>
      <div className="service-grid">
        <div className="service">
          <h3>Sanitation Companies</h3>
          <p>Eco-friendly waste management strategies and technologies</p>
        </div>
        <div className="service">
          <h3>Hospitals</h3>
          <p>Reducing environmental impact through smart facility management</p>
        </div>
        <div className="service">
          <h3>Universities</h3>
          <p>Green campus initiatives and eco-friendly academic practices</p>
        </div>
        <div className="service">
          <h3>Restaurants</h3>
          <p>Sustainable sourcing and waste reduction strategies</p>
        </div>
      </div>
</section>
    </div>
  );
};

export default HomePage;
