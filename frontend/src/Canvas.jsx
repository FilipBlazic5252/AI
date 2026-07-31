import { useRef, useEffect } from "react";
import API from "./api";
import { useState } from "react";

function Canvas({ setDigit, setConfidence }) {

    const canvasRef = useRef(null);

    const drawing = useRef(false);

    useEffect(() => {

        const canvas = canvasRef.current;
        const ctx = canvas.getContext("2d");

        // Black background
        ctx.fillStyle = "white";
        ctx.fillRect(0, 0, canvas.width, canvas.height);

        // White pen
        ctx.strokeStyle = "black";
        ctx.lineWidth = 10;
        ctx.lineCap = "round";
        ctx.lineJoin = "round";

    }, []);

    const getPosition = (e) => {

        const rect = canvasRef.current.getBoundingClientRect();

        return {
            x: e.clientX - rect.left,
            y: e.clientY - rect.top
        };

    };

    const startDrawing = (e) => {

        drawing.current = true;

        const ctx = canvasRef.current.getContext("2d");

        const pos = getPosition(e);

        ctx.beginPath();
        ctx.moveTo(pos.x, pos.y);

    };

    const draw = (e) => {

        if (!drawing.current) return;

        const ctx = canvasRef.current.getContext("2d");

        const pos = getPosition(e);

        ctx.lineTo(pos.x, pos.y);

        ctx.stroke();

    };

    const stopDrawing = () => {

        drawing.current = false;

    };

    const clearCanvas = () => {

        const canvas = canvasRef.current;

        const ctx = canvas.getContext("2d");

        ctx.fillStyle = "white";

        ctx.fillRect(0, 0, canvas.width, canvas.height);

        setDigit(null);
        setConfidence(null);
    };

    const predict = async () => {

        const canvas = canvasRef.current;

        canvas.toBlob(async (blob) => {

            const form = new FormData();

            form.append("file", blob, "digit.png");
            const response = await API.post(
                "/predict",
                form,
                {
                    headers: {
                        "Content-Type": "multipart/form-data"
                    }
                }
            );

            setDigit(response.data.digit);

            setConfidence(
                response.data.confidence + "%"
            );

        });

    };

    const [uploadingFile, setFile] = useState(null);

    const SaveFile = (e) => {
        setFile(e.target.files[0]);
        const imgFile = e.target.files[0];
        if (!imgFile) return;
        const img = new Image();
        img.onload = () => {
            const canvas = canvasRef.current;
            const ctx = canvas.getContext("2d");

            // Clear previous image
            ctx.clearRect(0, 0, canvas.width, canvas.height);

            // Draw image
            ctx.drawImage(
                img,
                0,
                0,
                canvas.width,
                canvas.height
            );
        };
        img.src = URL.createObjectURL(imgFile);
    }
    const handleChooseFile = () => {

        fileInputRef.current.click();

    };
    const fileInputRef = useRef(null);
    return (

        <>

            <canvas
                ref={canvasRef}
                width={280}
                height={280}

                onMouseDown={startDrawing}
                onMouseMove={draw}
                onMouseUp={stopDrawing}
                onMouseLeave={stopDrawing}

                style={{
                    border: "2px solid black",
                    background: "white",
                    cursor: "crosshair"
                }}
            />

            <br />
            <button onClick={handleChooseFile}>
                Select Image
            </button>
            <button onClick={predict}>
                Predict
            </button>

            <button onClick={clearCanvas}>
                Clear
            </button>

            <input type="file" onChange={SaveFile} hidden
                ref={fileInputRef} />


        </>

    );

}

export default Canvas;