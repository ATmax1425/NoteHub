function customiseUrl(imageUrl, size) {
    const googleDriveDomain = "drive.google.com";
    const googleUserContent = "lh3.googleusercontent.com";

    if(imageUrl.includes(googleDriveDomain)) {
        imageUrl = imageUrl.replace(/file\/d\//, "thumbnail?id=");
        imageUrl = imageUrl.replace(/\/view/, `&sz=s${size}`);
    } 
    else if(imageUrl.includes(googleUserContent)) {
        const pattern = /(?<=s)\d+(?=-c)/;
        imageUrl = imageUrl.replace(pattern, size);
    }

    return imageUrl;
}

function timeAgo(timestamp) {
    const now = new Date();
    const postDate = new Date(timestamp);
    const diffInSeconds = Math.floor((now - postDate) / 1000);

    const seconds = diffInSeconds;
    const minutes = Math.floor(diffInSeconds / 60);
    const hours = Math.floor(diffInSeconds / 3600);
    const days = Math.floor(diffInSeconds / 86400);
    const months = Math.floor(diffInSeconds / (86400 * 30.44));
    const years = Math.floor(diffInSeconds / (86400 * 365.25));

    if (years > 0) {
        return years === 1 ? "1 year ago" : `${years} years ago`;
    } else if (months > 0) {
        return months === 1 ? "1 month ago" : `${months} months ago`;
    } else if (days > 0) {
        return days === 1 ? "1 day ago" : `${days} days ago`;
    } else if (hours > 0) {
        return hours === 1 ? "1 hour ago" : `${hours} hours ago`;
    } else if (minutes > 0) {
        return minutes === 1 ? "1 minute ago" : `${minutes} minutes ago`;
    } else {
        return seconds === 1 ? "1 second ago" : `${seconds} seconds ago`;
    }
}