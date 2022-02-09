const ResultItem = ({ data }) => {
    const unit = data.unit !== "none" ? data.unit : "";
    const value = Number.isInteger(data.value) ? Math.round(data.value) : data.value.toFixed(2);

    return (
        <div className="resultitem">
            <p><b>({data.why})</b>: {data.description}</p>
            <p>{value} {unit} <i>(score: {data.score})</i></p>
        </div>
    )
}

export default ResultItem;