import useSearch from "../hooks/useSearch"
import "./results.css"

const ResultItem = ({ data }) => {
    return (
        <p><b>{data.why}</b>: {data.description}</p>
    )
}

const Results = ({ searchTerms }) => {
    const searchResults = useSearch(searchTerms);

    return (
        <div className="result transparentbox">
            {searchResults.map(e => <ResultItem data={e} />)}
        </div>
    )
}

export default Results;