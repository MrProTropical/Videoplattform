import React from 'react'
import "./RecommendedVideos.css"

function RecommendedVideos() {
    return (
        <div className="recommendedVideos">
            <h2>Recommended</h2>
            <div className="recommendedVideos__videos">
               <Video /> 
               <Video /> 
               <Video /> 
               <Video /> 
               <Video /> 
               <Video /> 
               <Video /> 
               <Video /> 
               <Video /> 
               <Video /> 
               
            </div>
        </div>
    )
}

export default RecommendedVideos