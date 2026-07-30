import React, { Component } from 'react'
import { BrowserRouter, Routes, Route } from 'react-router-dom'
import Screen from './Screen'
import Canvas from './Canvas'

export default class RoutedApp extends Component {

    render() {
        return (
            <>
                <BrowserRouter>
                    <Routes>
                        <Route path='/' Component={Screen} />
                        <Route path='/canvas' Component={Canvas} />
                    </Routes>
                </BrowserRouter>
            </>
        )
    }
}
